//  ----------
//  Прайс-лист
//  ----------

import {defineStore} from "pinia";

export const usePriceStore = defineStore("priceStore", () => {
    const products = ref([])
    const groups = ref([])
    const perPage = ref(1)
    const numPages = ref(1)
    const currentPage = ref(1)
    const count = ref(0)
    const search = ref(null)
    const price_min = ref(null)
    const price_max = ref(null)
    const page = ref(1)
    const group = ref(null)

    const getPriceList = async (is_root) => {
        const {data} = await useFetch(`/api/v1/prices`, {
            method: "POST",
            body: {
                payload: {
                    search: search.value,
                    price_min: price_min.value,
                    price_max: price_max.value,
                    page: page.value,
                    group: group.value
                }
            }
        })
        if (is_root === 1) {
            products.value = [];
        }
        if (data.value?.results) {
            const per_page = data.value?.results.per_page;
            const items = data.value?.results.results;
            if (is_root === undefined)
                products.value = items;
            else if (items.length > 0)
                products.value.push(... items);
            const size = products.value.length;
            const num_pages = Math.floor(size / per_page); 

            perPage.value = per_page;
            count.value = size;
            numPages.value = num_pages;
            currentPage.value = data.value?.results.current_page;
        } else if (data.value?.error) {
            console.log("getPriceList", data.value?.error)
            // TODO сделать вывод ошибок
        }
    }

    const getGroupTree = async () => {
        const {data} = await useFetch(`/api/v1/group_tree`)
        groups.value = data.value?.results
    }

    const getPriceDetail = async (id) => {
        const {data} = await useFetch('/api/v1/price_detail', {
            method: 'GET',
            query: {
                id: id,
            }
        })

        if (data.value?.results) {
            return data.value.results
        } else if (data.value?.error) {
            console.log("getPriceDetail", data.value?.error)
            // TODO сделать вывод ошибок
        }
    }

    const resetPagination = () => {
        page.value = 1
    }

    return {
        products,
        groups,
        perPage,
        numPages,
        currentPage,
        count,
        search,
        price_min,
        price_max,
        page,
        group,
        getPriceList,
        getGroupTree,
        getPriceDetail,
        resetPagination
    }
})
