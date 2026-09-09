from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import *

from database import get_expenses, add_expense
from keyboards import keyboard_menu, keyboard_category, keyboard_back_to_menu

router = Router()

class Data(StatesGroup):
    amount = State()
    category = State()
    comment = State()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer('🥸Меню\n\n'
                         'Выберите ниже действие☺️', reply_markup=keyboard_menu())

@router.callback_query(F.data == "help")
async def help(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text='❓❓❓\n\n'
                                          'Это бот для подсчётов расходов. Чтобы добавить расходы'
                                          'вам нужно нажать на кнопку "Добавить расходы".', reply_markup=keyboard_back_to_menu())

@router.callback_query(F.data == "statistic")
async def statistics(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    expenses = get_expenses(user_id)

    if not expenses:
        await callback.message.edit_text(text='У вас пока что нет расходов😔', reply_markup=keyboard_back_to_menu())
        return

    total = 0

    categories = {}

    for expense in expenses:
        expense_id, user_id, amount, category, comment, created_at = expense
        total += amount

        categories[category] = categories.get(category, 0) + amount

    text = (f"💰Общая сумма расходов: {total}\n\n")

    for category, amount in categories.items():
        name = category_name.get(category, category)
        text += f"{name}: 🤑{amount:.2f}\n"

    await callback.message.edit_text(text=text, reply_markup=keyboard_back_to_menu())

@router.callback_query(F.data == "expense")
async def start_FSM(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text(text='Напишите ниже сумму трат🤑')

    await state.set_state(Data.amount)

@router.message(Data.amount)
async def get_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите расходы числом!😡")
        return

    await state.update_data(amount=float(message.text))
    await message.answer(text='Выберите категорию🤓', reply_markup=keyboard_category())

    await state.set_state(Data.category)

category_name = {
    "Food": "🍔Еда",
    "Transport": "🚖Транспорт",
    "Entertainment": "🎭Развлечения",
    "Purchases": "🛒Покупки",
    "Others": "🔄Другое"
}

@router.callback_query(Data.category, F.data.startswith("category_"))
async def get_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    category = callback.data.split("_")[1]

    await state.update_data(category=category)

    await callback.message.edit_text(text='Добавьте заметку к расходам🙃')

    await state.set_state(Data.comment)

@router.message(Data.comment)
async def get_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)

    user_data = await state.get_data()

    user_id = message.from_user.id

    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    add_expense(user_id, user_data['amount'], user_data['category'], user_data['comment'], created_at)


    await message.answer(f"✅ Расходы сохранились.\n\n"
                         f"💰Сумма: {user_data['amount']}\n"
                        f"🤓Категория: {user_data['category']}\n"
                        f"📆Дата: {created_at}", reply_markup=keyboard_back_to_menu())

    await state.clear()

@router.callback_query(F.data == "history")
async def history(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    expenses = get_expenses(user_id)

    if not expenses:
        await callback.message.edit_text(text="⏳История расходов\n\n"
                                         "У вас пока нет расходов.😞", reply_markup=keyboard_back_to_menu())

        return

    text = "⏳История расходов\n\n"

    for expense in expenses:
        expense_id, user_id, amount, category, comment, created_at = expense

        name = category_name.get(category, category)

        text += f"💰 {amount} - {name}\n"
        text += f"😶Комментарий: {comment}\n"
        text += f"📆Дата: {created_at}\n\n"

    await callback.message.edit_text(text=text, reply_markup=keyboard_back_to_menu())

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text='🥸Меню\n\n'
                                          'Выберите действие☺️', reply_markup=keyboard_menu())