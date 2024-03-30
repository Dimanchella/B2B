export default defineEventHandler(async (event) => {
    const {page} = await getQuery(event)
    const url = "/backend/api/v1/orders/"
    return await $fetch(
        `${process.env.DJANGO_URL}${url}`,
        {
            method: "GET",
            headers: event.context.headers,
            query: {
                page
            }
        }
    ).catch((err) => {
        if (err.data?.error?.code >= 400) {
            return err.data
        }
    })
})