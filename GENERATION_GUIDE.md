# Инструкция: что сгенерить в Higgsfield для рилса v3

Всего нужно 2 обязательных клипа и 2 опциональных. Каждый — image-to-video,
5 секунд; в монтаж из каждого пойдёт 1–2 лучшие секунды. Обе картинки
для обязательных клипов уже лежат в вашей медиатеке Higgsfield (и продублированы
файлами в чате: likho_camp.jpg и likho_mask.jpg).

Общие настройки для всех генераций:
- режим **image-to-video** (картинка как стартовый кадр);
- модель **Kling 3.0 Turbo** (быстрая, хорошо держит стартовый кадр);
  если результат мыльный — перегенерить на Kling 3.0 обычном;
- длительность **5 сек**, aspect ratio оставить как у картинки;
- в промптах всегда стоит «no text» — если модель всё же дорисует буквы,
  просто перегенерите.

---

## Клип 1 (обязательный) — «PDF дышит»

**Куда в рилсе:** 0:01–0:02, на фразу «Сначала оно было только в PDF».
Смысл: нарисованное уже шевелится — зритель чувствует неладное до матч-ката.

1. Откройте image-to-video, выберите картинку кэмпа (рендер с чёрным котом).
2. Промпт:

```
The huge white fabric pavilion slowly breathes like a sleeping creature:
translucent tulle ripples and billows gently in the wind, morning fog
drifts low across the field, warm golden dawn light flickers, a black cat
walks through the grass. Subtle slow camera push-in.
Dreamy mystical cinematic realism, no text, no captions.
```

3. Что взять в монтаж: 1–1,5 сек, где ткань движется заметнее всего.
4. Критерий брака: ткань «плывёт» как жидкость, люди деформируются →
   перегенерить, в промпт добавить `people stay still`.

## Клип 2 (обязательный) — «рендер маски оживает»

**Куда в рилсе:** 0:02–0:03, кадр ПЕРЕД match-cut «оно открыло глаза».
Наезд на нарисованную маску → склейка в реальную маску с того же ракурса.

1. Image-to-video, картинка шествия с маской (аэросъёмка, вуаль, красные ленты).
2. Промпт:

```
Aerial view: ghostly white veiled procession creature with a horned mask
drifts very slowly across a misty golden field, translucent fabric
billowing softly, red ribbons fluttering in the wind.
Slow steady camera push-in toward the mask face.
Mystical folk-tale mood, cinematic, no text, no captions.
```

3. Что взять в монтаж: последние ~1,5 сек наезда, где маска уже крупно —
   финальный кадр этого клипа и есть точка склейки с вашим реальным фото
   маски (выравнивайте по глазам).
4. Критерий брака: маска меняет форму/лицо при наезде → перегенерить
   с добавкой `the mask shape stays identical, rigid solid mask`.

## Клип 3 (опциональный, но очень сильный) — «глаза загораются»

**Куда в рилсе:** 0:03–0:04, сразу ПОСЛЕ матч-ката — реальная маска
«просыпается». Если получится — это самый пересматриваемый кадр.

1. Загрузите в Higgsfield ВАШЕ реальное фото маски крупным планом
   (то, где морда на фоне неба, снизу вверх).
2. Image-to-video, промпт:

```
The giant white mask slowly comes alive: a faint warm glow appears deep
inside the empty eye sockets, fabric around the mask stirs in the wind,
clouds move slowly behind. The mask itself stays perfectly rigid and
does not change shape. Subtle ominous awakening, cinematic, no text.
```

3. Что взять: момент появления свечения, 1–1,5 сек.
4. Критерий брака: маска начинает «говорить»/мимировать → добавить
   `no facial movement, the mask is solid plaster`.

## Клип 4 (опциональный) — «скелет провожает»

**Куда в рилсе:** финал 0:16–0:17, пустой каркас перед возвратом на маску.

1. Загрузите ваше реальное фото голого каркаса (или рендер со стр. 16
   альбома — страница с каркасом в тумане).
2. Промпт:

```
Bare white skeletal frame of arched tubes stands in a misty field at dusk,
thin fog slowly rolls between straw blocks, grass sways gently.
Empty, cold, abandoned mood. Static camera, very subtle motion,
cinematic, no text.
```

3. Что взять: любые 1–1,5 сек — движение тумана делает кадр «живым мёртвым».

---

## Что НЕ генерить

- **Музыку** — Higgsfield делает только речь. Трек берём в CapCut:
  тревожный ритмичный, вступает ударом на матч-кате (см. сценарий v3).
- **Шествие и стройку** — у вас есть настоящие кадры, они сильнее любого AI.
  Генерация нужна только там, где камеры не было: ожившие рендеры.
- **Реальные сцены фестиваля «получше»** — подмена реальности AI-кадрами
  считывается и убивает доверие к истории «мы правда это построили».

## Куда сложить результат

Скачайте клипы в галерею телефона → в CapCut они встают в таймлайн v3
на места из колонки «Куда в рилсе». После сборки черновика — присылайте
сюда, прогоню по чек-листу сценария.
