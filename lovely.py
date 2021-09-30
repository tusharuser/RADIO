#import logging
import os
import signal
import ffmpeg  
from pyrogram import Client, filters
from pytgcalls import GroupCall




API_ID = 2643895
API_HASH = "d304742e89bf3b4058e3d0887bcc22da"
SESSION_NAME = "AQDEcKbZRWLZUNttlKrjjU5_vjTat96Y1wewMzpciO2FZjcdu5n7B8bpsl9Y7rvYWhVP5xHpOkOjCHyT1mxXS-YuaPWkFLO5yqQPZIQUTDtTVbEchRGIlYjMUnh-fpeG4UnvQzMT5XLCAXfiI0l3Uo_4WDJH6ZdOr4iiJzlfpxquD8FrjIg61LVP0LximuMlJVSPc7gAzySOKimRhi7iXfc3NN2gDkbFjYlP3UDkTFUuY_cFvYqgDeHZSkKTmNIX06wLLeYx2THfvSrpyVY6PkBaRIhceant9KTxdluNRiBW916thbIZDUVLThhf2HagGTPv7WUYidhFfuB7J7ZUsxNdVz5nuAA"


app = Client(SESSION_NAME, API_ID, API_HASH)
#logging.basicConfig(level=logging.INFO)



HELP =""" Lovely Radio stations:

1. https://radioindia.net/radio/hungamanow/icecast.audio

2. https://filmymirchihdliv-lh.akamaihd.net/i/FilmyMirchiHDLive_1_1@336266/master.m3u8

3. https://radioindia.net/radio/mirchi98/icecast.audio

4. https://radioindia.net/radio/hungamanow/icecast.audio

ᴛᴏ ꜱᴛᴀʀᴛ ʀᴇᴘʟᴀʏ ᴛᴏ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ ᴄᴏᴍᴍᴀɴᴅ /lovely <Station Number> ʟɪᴋᴇ /lovely 1
ᴛᴏ ᴇɴᴅ and ꜱᴛᴏᴘ ꜱᴛʀᴇᴀᴍ by /stop ᴄᴏᴍᴍᴀɴᴅ  for any help join @LOVELY_5UPPORT """


GROUP_CALLS = {}
FFMPEG_PROCESSES = {}

@app.on_message(filters.command('help',prefixes='/'))
async def help(client,message):
	get =await client.get_chat_member(message.chat.id,message.from_user.id)
	status = get. status
	cmd_user = ["administrator","creator"]
	if status in cmd_user:
		await message.reply_text(HELP)


@app.on_message(filters.command('lovely', prefixes='/'))
async def start(client,message):
	get =await client.get_chat_member(message.chat.id,message.from_user.id)
	status = get. status
	cmd_user = ["administrator","creator"]
	if status in cmd_user:
		input_filename = f'radio-{message.chat.id}.raw'
		group_call = GROUP_CALLS.get(message.chat.id)
		if group_call is None:
		      group_call = GroupCall(client, input_filename, path_to_log_file='')
		      GROUP_CALLS[message.chat.id] = group_call
		if not message.reply_to_message or len(message.command) < 2:
		      await message.reply_text('You forgot to replay list of stations or pass a station ID')
		      return
	process = FFMPEG_PROCESSES.get(message.chat.id)
	if process:
		process.send_signal(signal.SIGTERM)
	station_stream_url = None
	station_id = message.command[1]
	msg_lines = message.reply_to_message.text.split('\n')
	for line in msg_lines:
	       line_prefix = f'{station_id}. '
	       if line.startswith(line_prefix):
	           station_stream_url = line.replace(line_prefix, '').replace('\n', '')
	           break
	if not station_stream_url:
	       await message.reply_text(f'Can\'t find a station with id {station_id}')
	       return
	await group_call.start(message.chat.id)
	process = ffmpeg.input(station_stream_url).output(        input_filename, format='s16le',       acodec='pcm_s16le', ac=2, ar='48k'  ).overwrite_output().run_async()
	FFMPEG_PROCESSES[message.chat.id] = process
	await message.reply_text(f'RADIO #{station_id} ꜱᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ ᴜʀ ᴄʜᴏᴏꜱᴇɴ ꜱᴛᴀᴛɪᴏɴ JOIN @LOVELY_NETWORK.')


@app.on_message( filters.command('stop', prefixes='/'))
async def stop(client,message):
	get =await client.get_chat_member(message.chat.id,message.from_user.id)
	status = get. status
	cmd_user = ["administrator","creator"]
	if status in cmd_user:
	   group_call = GROUP_CALLS.get(message.chat.id)
	   if group_call:
	   	await group_call.stop()
	   process = FFMPEG_PROCESSES.get(message.chat.id)
	   if process:
	   	process.send_signal(signal.SIGTERM)
	   





app.run()

