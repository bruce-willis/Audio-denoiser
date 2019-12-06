# Audio denoiser


- [Что есть и как попробовать:](#что-есть-и-как-попробовать)
- [Обучение](#обучение)
- [Заметки](#заметки)


### Что есть и как попробовать:
* Установить исходную версию [spleeter](https://github.com/deezer/spleeter/wiki/1.-Installation)
* Проверить, что все установлено правильно: [`usage/LoadPythonExample.ipynb`](https://nbviewer.jupyter.org/github/bruce-willis/Audio-denoiser/blob/develop/src/usage/LoadPythonExample.ipynb)
* Скачать данные [отсюда](https://drive.google.com/open?id=1xSLmBHS8iUQUu85dNknrg8ifxrmvsfRW). BTW: очень удобно скачивать с gdrive при помощи [этой утилиты](https://github.com/GitHub30/gdrive.sh)
* Распаковать в папку в корне `data`
* Проверить исходную модель на произвольной дорожке: [`usage/CheckSpeach.ipynb`](https://nbviewer.jupyter.org/github/bruce-willis/Audio-denoiser/blob/develop/src/usage/CheckSpeach.ipynb).


### Обучение
* исходный spleeter был написан на tensorflow версии 1, но код неплохой, используется `tf.estimator`
* [инструкция](https://github.com/deezer/spleeter/wiki/2.-Getting-started#train-model) только для cli обучения, но когда отсутствие инструкции останавливало?)
* Подготовка:
    * нужно подготовить `csv` с путями до аудио для `train` и `test`: [`training/1_dataset_preparation.ipynb`](training/1_dataset_preparation.ipynb). Также, из-за непонятной мне причины, нужно **обязательно** конвертировать в 44.1к sample_rate и стерео. ¯\\_(ツ)_/¯
    * подредактировать `config` со всеми параметрами модели и путями до `csv`: [`training/config/voice_config.json`](training/config/voice_config.json)
* Поставить дообучаться на этом датасете: [`training/2_model_training.ipynb`](`training/2_model_training.ipynb`)
* ???
* **PROFIT!**


### Заметки
* модель от Deezer работает не очень, получается крайне тихий и чутка «размазанный» голос
* было бы клёво не обучать с нуля модель, а использовать готовые веса. Но, к сожалению, пока это не так уж и [просто](https://github.com/deezer/spleeter/issues/32#issuecomment-557146776) :(
* можно разительно увеличить размер датасета, перемешивая случайным образом шум и голос

