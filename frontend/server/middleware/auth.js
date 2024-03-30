import {getToken} from '#auth'

export default defineEventHandler(async (event) => {
    const token = await getToken({event})
    event.context.headers = {
        "content-type": "application/json",
        "Authorization": `Bearer ${token?.accessToken}`
    }
})