//  -------
//  Корзина
//  -------

import {defineStore} from "pinia";

export const useCartStore = defineStore("cartStore", () => {
    const cart = ref([])
    const addToCart = (product) => {
        const index = cart.value.findIndex(item => item.id === product.id)
        if (index >= 0) {
            cart.value[index].count++
        } else {
            product.count = 1
            cart.value.push(product)
        }
    }

    const changeFromCart = (product, value) => {
        if (isNaN(value)) {
            const message = "ERROR!\nProduct count value should be a number only\nPlease, repeat";
            alert(message);
            return false;
        }
        const save = product.count || 0;
        const count = Number(value);
        //console.log('Cart:', cart);
        product.count = count;
        const index = cart.value.findIndex(item => item.id === product.id)
        if (index > -1) {
            cart.value[index].count = count;
        } else {
            cart.value.push(product);
        }
        //console.log('Product:', product);
    }

    const deleteFromCart = (product) => {
        const index = cart.value.findIndex(item => item.id === product.id)
        if (index < 0) return
        if (cart.value[index].count > 0) {
            cart.value[index].count--
        }
        if (cart.value[index].count === 0) {
            cart.value.splice(index, 1)
        }
    }

    const deleteProductFromCart = (product) => {
        const index = cart.value.findIndex(item => item.id === product.id)
        if (index < 0) return
        cart.value[index].count = 0
        cart.value.splice(index, 1)
    }

    const clearCart = () => {
        cart.value = []
    }

    const cartCount = () => {
        return cart.value.reduce((acc, item) => {
            return acc + item.count
        }, 0)
    }

    const productCount = (product) => {
        const index = cart.value.findIndex(item => item.id === product.id)
        if (index >= 0) {
            return cart.value[index].count
        }

        return 0
    }

    const uniProductsCount = () => {
        return cart.value.length
    }

    const cartSum = () => {
        //console.log('cart: ', cart);
        const sum = cart.value.reduce((acc, item) => {
            return acc + Number(isNaN(item.price) ? 0 : item.price) * item.count;
        }, 0);

        return sum.toLocaleString(undefined, {minimumFractionDigits: 2});
    }

    const emptyCart = () => {
        return cart.value.length === 0
    }

    const createNewOrder = async () => {
        const {data} = await useFetch("/api/v1/orders", {
            method: "POST",
            body: {
                payload: {
                    from_frontend: true
                }
            }
        })

        if (data.value?.results) {
            orders.value.unshift(data.value?.results)
        } else if (data.value?.error) {
            console.log("createNewOrder", data.value?.error)
            // TODO сделать вывод ошибок
        }
    }

    return {
        cart,
        addToCart,
        changeFromCart,
        deleteFromCart,
        deleteProductFromCart,
        clearCart,
        cartCount,
        productCount,
        uniProductsCount,
        cartSum,
        emptyCart
    }
}, {
    persist: true,
})

