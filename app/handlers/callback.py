from aiogram import Bot
from aiogram.types import CallbackQuery


async def select_info(call: CallbackQuery, bot: Bot):
    data = call.data
    if data == "wallet_info":
        answer = (
            "Для того чтобы создать кошелeк вам нужно следовать следующей инструкции мы рекомендуем устанавливать "
            "кошелек tonkeeper(так же можно воспользоваться кошельком от телеграма): \n"
            "1. Перейти на сайт https://tonkeeper.com/ и установить кошелек на устройство \n"
            "2. Нажимаем кнопку подключить кошелек \n"
            "3. Нажимаем кнопку создать новый кошелек \n"
            "4. Сохраняем сид-фразу (обязательно сохраните для дальнейшего доступа к кошельку) \n"
            "5. Подтверждаем правильность сид-фразы \n"
            "6. Создайте секретный пин-код для доступа к кошельку \n"
            "7. Поздравляем! Ваш кошелек готов"
        )
    elif data == "about":
        answer = (
            "Уральский сад лечебных культур им.проф. Л.И. Вигорова - это ботанический сад УГЛТУ с уникальной "
            "коллекцией древесных растений, накапливающих в различных органах биологически активные вещества (БАВ) в "
            "эффективных колличествах. Сад был заложен в 1950 году профессором Леонидом Ивановичем Вигоровым."
        )

    await call.message.answer(answer)
    await call.answer()