export default defineEventHandler(async (event) => {
    const {payload} = await readBody(event)

    console.log(payload)

    const url = "/backend/api/v1/orders/"

    return await $fetch(
        `${process.env.DJANGO_URL}${url}`,
        {
            method: "POST",
            headers: event.context.headers,
            body: payload
        }
    ).catch((err) => {
        console.log(err)
        if (err.data?.error?.code >= 400) {
            return err.data
        }
    })
})