export default defineEventHandler(async (event) => {
    let url = "/backend/api/v1/products_groups_tree/"
    return await $fetch(`${process.env.DJANGO_URL}${url}`)
})