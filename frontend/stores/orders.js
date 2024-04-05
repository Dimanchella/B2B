import {defineStore} from "pinia";

export const useOrderStore = defineStore("orderStore", () => {
    const orders = ref([])
    const perPage = ref(1)
    const numPages = ref(1)
    const currentPage = ref(1)
    const count = ref(0)
    const page = ref(1)

    const getOrderList = async () => {
        const {data} = await useFetch("/api/v1/orders", {
            method: "GET",
            query: {page: page.value}
        })

        if (data.value?.results) {
            count.value = data.value?.results.count
            numPages.value = data.value?.results.num_pages
            perPage.value = data.value?.results.per_page
            currentPage.value = data.value?.results.current_page
            orders.value = data.value?.results.results
        } else if (data.value?.error) {
            console.log("getOrderList", data.value?.error)
            // TODO сделать вывод ошибок
        }
    }

    const getOrder = async (id) => {
        const {data} = await useFetch("/api/v1/order/", {
            method: "GET",
            query: {id: id}
        })

        // console.log(data.value)

        return data
    }

    const createNewOrder = async (cart) => {
        //console.log(cart);
        const {data} = await useFetch("/api/v1/create_new_order", {
            method: "POST",
            body: {payload: cart}
        })

        if (data.value?.results) {
            return data.value?.results?.id
        } else if (data.value?.error) {
            console.log("createNewOrder", data.value?.error)
            // TODO сделать вывод ошибок
        }
    }

    const updateOrder = async (order, register) => {
        // Обновить данные заказа
        if (register && order.value.site_status === "CR") {
            order.value.site_status = "WR"
        }

        // XXX
        order.value.from_frontend = true
        const {data} = await useFetch("/api/v1/order", {
            method: "PUT",
            query: {
                id: order.value.id,
            },
            body: {payload: order.value}
        })
    }

    const deleteOrder = async (item) => {
        const {data} = await useFetch("/api/v1/orders", {
            method: "DELETE",
            query: {
                id: item.id
            }
        })

        const result = orders.value.findIndex(arrItem => arrItem.id === item.id)
        if (result !== undefined) {
            orders.value.splice(result, 1)
        }
    }

    const orderCount = (order) => {
        return order.order_orders_detail.reduce((acc, item) => {
            return acc + Number(item.quantity)
        }, 0)
    }

    const uniProductsCount = (order) => {
        // console.log("uniProductsCount: ", order, order.order_orders_detail)
        return order.order_orders_detail.length
    }

    const orderSum = (order) => {
        const sum = order.order_orders_detail.reduce((acc, item) => {
            return acc + Number(item.total)
        }, 0)

        return sum.toLocaleString(undefined, {minimumFractionDigits: 2})
    }

    return {
        orders,
        perPage,
        numPages,
        currentPage,
        count,
        page,
        getOrderList,
        getOrder,
        createNewOrder,
        updateOrder,
        deleteOrder,
        orderCount,
        orderSum,
        uniProductsCount
    }
})
