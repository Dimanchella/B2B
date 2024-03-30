export default (status) => {
    if (status === 'CR') return 'Создан'
    else if (status === 'WR') return 'В обработке'
    else if (status === 'PR') return 'Обработан'
    else if (status === 'CL') return 'Закрыт'
    else return 'Неизвестный'
}
