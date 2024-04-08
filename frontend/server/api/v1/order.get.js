export default defineEventHandler(async (event) => {

    const {id} = getQuery(event)

    const url = `/backend/api/v1/orders/${id}/`

    return await $fetch(
        `${process.env.DJANGO_URL}${url}`,
        {
            method: "GET",
            headers: event.context.headers,
        }).catch((err) => {
        if (err.data?.error?.code >= 400) {
            return err.data
        }
    })
})
