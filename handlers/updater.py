from rest_framework.response import Response
from rest_framework.views import APIView
from aiogram import types, Dispatcher, Bot
from loader import dp
import asyncio


loop = asyncio.get_event_loop()

class UpdateBot(APIView):
    def post(self,request):
        try:
            update = types.Update(**request.data)
            Dispatcher.set_current(dp)
            Bot.set_current(dp.bot)
            loop.run_until_complete(dp.process_update(update))
        except Exception as e:
            print(e)
        finally:
            return Response(status=200)