import asyncio
import openai
import aiogram
from settings import OPENAI_TOKEN


class ChatGPTService:

    openai.api_key = OPENAI_TOKEN

    async def complete(self,
                       message: aiogram.types.Message,
                       stream: bool = False):

        send_completion_method = self.send_streamed_completion if stream \
            else self.send_completion

        task = asyncio.ensure_future(
            send_completion_method(message)
        )
        # For 'Bot is typing...'
        while not task.done():
            await message.answer_chat_action(aiogram.types.ChatActions.TYPING)
            await asyncio.sleep(4)

    async def send_streamed_completion(self,
                                       prompt_message: aiogram.types.Message):

        initial_message = await prompt_message.answer('...')
        await initial_message.answer_chat_action(
            aiogram.types.ChatActions.TYPING)

        completion = await self._get_completion(
            prompt=prompt_message.text,
            stream=True
        )

        message_text = ''
        async for chunk in completion:
            content = chunk.choices[0].delta.get('content', None)
            if not content:
                continue
            message_text += content
            # Avoid RetryAfter Flood Exception
            await asyncio.sleep(0.50)
            try:
                await initial_message.edit_text(message_text)
            except Exception:
                continue

        cleanup_chat_action_msg = await initial_message.answer('...')
        await cleanup_chat_action_msg.delete()

    async def send_completion(self,
                              prompt_message: aiogram.types.Message):

        completion = await self._get_completion(
            prompt=prompt_message.text,
            stream=False
        )
        await prompt_message.answer(
            completion.choices[0].message['content'])

    async def _get_completion(self,
                              prompt: str,
                              stream: bool):
        return await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                    {
                     "role": "user",
                     "content": prompt
                    }
                ],
            stream=stream
        )
