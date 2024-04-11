
export default defineEventHandler(async (event) => {

    const {payload} = await readBody(event)

    const url = "/backend/api/v1/create_new_order/"

    console.log(payload);

    return await $fetch(
        `${process.env.DJANGO_URL}${url}`,
        {
            method: "POST",
            headers: event.context.headers,
            body: payload
        }).catch((e) => {
        console.log(e)
    })
})
