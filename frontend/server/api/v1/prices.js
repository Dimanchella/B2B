export default defineEventHandler(async (event) => {
    const {payload} = await readBody(event)

    let url = "/backend/api/v1/prices/"
    let params = []

    if (payload.search) {
        params.push(`search=${payload.search}`)
    }
    if (payload.page) {
        params.push(`page=${payload.page}`)
    }
    if (payload.group) {
        params.push(`group=${payload.group}`)
    }
    if (payload.price_min) {
        params.push(`price_min=${payload.price_min}`)
    }
    if (payload.price_max) {
        params.push(`price_max=${payload.price_max}`)
    }

    if (params.length > 0) {
        url += '?' + params.join('&')
    }

    return await $fetch(`${process.env.DJANGO_URL}${url}`)
})