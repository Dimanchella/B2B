export default defineEventHandler(async (event) => {

    const {id} = await getQuery(event)

    let url = '/backend/api/v1/price_detail/'
    let params = []

    if (id) {
        params.push(`id=${id}`)
    }

    if (params.length > 0) {
        url = url + '?' + params.join('&')
    }

    return await $fetch(
        `${process.env.DJANGO_URL}${url}`,
        {
            method: 'GET',
            headers: event.context.headers,
        }).catch((err) => {
        if (err.data?.error?.code === 401) {
            return err.data
        }
    })
})
