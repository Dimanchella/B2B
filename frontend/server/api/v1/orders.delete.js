export default defineEventHandler(async (event) => {
    const {id} = getQuery(event)

    const url = `/backend/api/v1/orders/${id}/`

    return await $fetch(
        `${process.env.DJANGO_URL}${url}`,
        {
            method: "DELETE",
            headers: event.context.headers
        }
    ).catch((err) => {
        console.log(err)
        if (err.data?.error?.code >= 400) {
            return err.data
        }
    })
})