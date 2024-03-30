export const useMessageStore = defineStore('messageStore', () => {

    let loading = ref(false)
    let error = ref(false)
    let message = ref(null)

    const clearMessage = () => {
        error = false
        message = null
    }

    const setMessage = (payload) => {
        error = false
        message = payload
    }

    const setError = (payload) => {
        error = true
        message = payload
    }

    return { loading, message, error, clearMessage, setMessage, setError }
})


