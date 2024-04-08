export default defineEventHandler(async (event) => {
    const {id} = await getQuery(event)
    const {payload} = await readBody(event)

    const url = `/backend/api/v1/orders/${id}/`

    return await $fetch(
        `${process.env.DJANGO_URL}${url}`,
        {
            method: "PUT",
            headers: event.context.headers,
            body: payload
        }).catch((e) => {
        console.log(e)
    })
})
