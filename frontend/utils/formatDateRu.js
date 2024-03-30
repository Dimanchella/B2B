export default (formatDate, now) => {
    if (!formatDate) return ''
    let docDate = new Date(formatDate).toLocaleString('ru', {year: 'numeric', month: 'numeric', day: 'numeric'})

    if (now === docDate) {
        return new Date(formatDate).toLocaleString('ru', {hour: 'numeric', minute: 'numeric'})
    } else {
        return docDate
    }
}
