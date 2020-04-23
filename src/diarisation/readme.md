# Spleeter for speaker separation
Или ещё одно подтверждение, что не существует серебряной пули.  

***

**TL;DR**: spleeter вообще не годится для данной задачи

***

Spleeter [позволяет](https://github.com/deezer/spleeter/blob/ca938960f438fa940f9b03860372a6ce61b4cb7c/spleeter/model/__init__.py#L26-L28) задавать архитектуру модели через конфигурацию, [например](https://github.com/deezer/spleeter/blob/ca938960f438fa940f9b03860372a6ce61b4cb7c/configs/2stems/base_config.json#L25).  

Горькая правда в том, что ни одна из этих архитектур не подходит, из-за ключевого решения: в оригинале тренируется по модели на каждый инструмент, что не подходит совсем для задачи разделения спикеров:
* [unet](https://github.com/deezer/spleeter/blob/ca938960f438fa940f9b03860372a6ce61b4cb7c/spleeter/model/functions/unet.py#L8-L10)
> *Each instrument is modeled by a single U-net* convolutional/deconvolutional network that take a mix spectrogram as input and the estimated sound spectrogram as output.
* [blstm](https://github.com/deezer/spleeter/blob/ca938960f438fa940f9b03860372a6ce61b4cb7c/spleeter/model/functions/blstm.py#L13-L17)
> *For each instrument, a network is trained* which predicts the target instrument amplitude from the mixture amplitude in the STFT domain. The raw output of each network is then combined by a multichannel Wiener filter.

Это подходит, когда требуется отделить разно звучащие инструменты (и в таком случае вполне оправданно учить отдельные модели), но не подходит для разделения говорящих (так как люди говорят ± одинаково, и нужна одна сеть с несколькими выходами).

***

Однако, я всё равно обучил каждую из конфигураций. Для подготовки тренировочного датасета, я брал две случайные дорожки и накладывал их друг на друга со случайным смещением 1-5 секунд — [`1_dataset_preparation.ipynb`](1_dataset_preparation.ipynb) (и такой подход вроде вполне оправдан, можно ещё менять громкость дорожек).

1. Обучение `unet` модели находится в [`2.0_unet_model_training.ipynb`](2.0_unet_model_training.ipynb), а послушать можно через [`nbviewer`](https://nbviewer.jupyter.org/github/bruce-willis/Audio-denoiser/blob/d1d397f22361d7930f99cb194b636988abdc59e7/src/diarisation/3.0_unet_check_speech.ipynb) — не работает **совсем**.

2. Обучение `blstm` модели находится в [`2.1_blstm_model_training.ipynb`](2.1_blstm_model_training.ipynb), а послушать можно через [`nbviewer`](https://nbviewer.jupyter.org/github/bruce-willis/Audio-denoiser/blob/d1d397f22361d7930f99cb194b636988abdc59e7/src/diarisation/3.1_blstm_check_speech.ipynb) — работает лучше предыдущего подхода, но все равно так себе качество.