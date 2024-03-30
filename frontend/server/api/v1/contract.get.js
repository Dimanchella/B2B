export default defineEventHandler(async (event) => {

    const url = '/backend/api/v1/contracts/'

    const resp = await $fetch(
        `${process.env.DJANGO_URL}${url}`,
        {
            method: 'get',
            headers: event.context.headers,
        }).catch((err) => {
        if (err.data?.error?.code === 401) {
            return err.data
        }
    })

    return resp
})
