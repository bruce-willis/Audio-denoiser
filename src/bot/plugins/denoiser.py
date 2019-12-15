import urllib.request
import uuid
from os import environ
from pathlib import Path

from kutana import Plugin, Environment
from kutana.manager.tg.environment import TGEnvironment, TGAttachmentTemp
from kutana.manager.vk.environment import VKEnvironment
from kutana.plugin import Message, Attachment

plugin = Plugin(name="Denoiser")


@plugin.on_startup()
async def initiation(kutana):
    from spleeter.audio.adapter import get_default_audio_adapter
    from spleeter.separator import Separator

    environ["GITHUB_REPOSITORY"] = "bruce-willis/Audio-denoiser"
    environ["GITHUB_RELEASE"] = "v0.1"

    config_url = "https://raw.githubusercontent.com/bruce-willis/Audio-denoiser/develop/src/training/config/voice_config.json"
    config_path = "voice_config.json"
    _ = urllib.request.urlretrieve(url=config_url, filename=config_path)

    separator = Separator(config_path)
    predictor = separator._get_predictor()
    plugin.predictor = predictor

    adapter = get_default_audio_adapter()
    plugin.adapter = adapter


def process_audio(filename):
    from spleeter.audio.convertor import to_stereo
    adapter = plugin.adapter
    waveform, sample_rate = adapter.load(str(filename))
    if not waveform.shape[-1] == 2:
        waveform = to_stereo(waveform)
    prediction = plugin.predictor({
        'waveform': waveform,
        'audio_id': ''})
    _ = prediction.pop('audio_id')
    predicted_voice_path = str(filename.parent / "voice.mp3")
    plugin.adapter.save(predicted_voice_path, prediction['voice'], sample_rate)
    predicted_noise_path = str(filename.parent / "noise.mp3")
    plugin.adapter.save(predicted_noise_path, prediction['noise'], sample_rate)
    return predicted_voice_path, predicted_noise_path


async def send_instruction_info(env: Environment):
    await env.reply("Отправь мне аудиосообщение!")


@plugin.on_message()
async def apply_denoiser(message: Message, env: Environment):
    folder_name = str(uuid.uuid4())
    filepath = Path("tmp") / folder_name
    filepath.mkdir(exist_ok=True, parents=True)
    original_filename = filepath / "original.ogg"

    if isinstance(env, TGEnvironment):
        try:
            file_id = message.raw_update["message"]["voice"]["file_id"]
        except:
            await send_instruction_info(env)
            return

        file_tg = await env.manager.request("getFile", file_id=file_id)
        file_content = await env.manager.request_file(file_tg.response["file_path"])

        with open(original_filename, mode="w+b") as fp:
            fp.write(file_content)

        voice_path, noise_path = process_audio(original_filename)

        with open(voice_path, "rb") as fh:
            voice_message = TGAttachmentTemp("voice", fh.read(), {})
        with open(noise_path, "rb") as fh:
            noise_message = TGAttachmentTemp("voice", fh.read(), {})

    elif isinstance(env, VKEnvironment):
        if not message.attachments or message.attachments[0].type != "audio_message":
            await send_instruction_info(env)
            return

        attachment: Attachment = message.attachments[0]
        file_link = attachment.raw_attachment["audio_message"]["link_ogg"]
        _ = urllib.request.urlretrieve(url=file_link, filename=original_filename)
        voice_path, noise_path = process_audio(original_filename)

        with open(voice_path, "rb") as fh:
            voice_message = await env.upload_doc(fh.read(), type="audio_message", filename="voice.ogg")
        with open(noise_path, "rb") as fh:
            noise_message = await env.upload_doc(fh.read(), type="audio_message", filename="noise.ogg")

    await env.reply("Cleaned voice", attachment=voice_message)
    await env.reply("Separated noise", attachment=noise_message)
    await env.reply("Готово, обращайся ещё!")
