export const useCatalogsStore = defineStore('catalogsStore', () => {

    const organization = ref([])
    const counterparty = ref([])
    const agreement = ref([])
    const contract = ref([])

    const getOrganization = async () => {
        const {data} = await useFetch('/api/v1/organization')
        organization.value = data.value?.results
        console.log('organization:', data)
    }

    const getCounterparty = async () => {
        const {data} = await useFetch('/api/v1/counterparty')
        counterparty.value = data.value?.results
        console.log('counterparty:', data)
    }

    const getAgreement = async () => {
        const {data} = await useFetch('/api/v1/agreement')
        agreement.value = data.value?.results
        console.log('agreement:', data)
    }

    const getContract = async () => {
        const {data} = await useFetch('/api/v1/contract')
        contract.value = data.value?.results
        console.log('contract:', data)
    }

    return {organization, counterparty, agreement, contract, getOrganization, getCounterparty, getAgreement, getContract}
})


