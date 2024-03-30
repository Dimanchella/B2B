export default defineEventHandler(async (event) => {
    let url = "/backend/api/v1/products_group_tree/"
    return await $fetch(`${process.env.DJANGO_URL}${url}`)
})