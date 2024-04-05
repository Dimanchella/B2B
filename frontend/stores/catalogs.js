export const useCatalogsStore = defineStore('catalogsStore', () => {

    const organization = ref([])
    const contractor = ref([])
    const partner = ref([])
    const agreement = ref([])
    const contract = ref([])

    const getOrganization = async () => {
        const {data} = await useFetch('/api/v1/organization')
        organization.value = data.value?.results
        // console.log('organization:', data)
    }

    const getContractor = async () => {
        const {data} = await useFetch('/api/v1/contractor')
        contractor.value = data.value?.results
        // console.log('contractor:', data.value?.results)
    }

    const getPartner = async () => {
        const {data} = await useFetch('/api/v1/partner')
        partner.value = data.value?.results
        // console.log('partner:', data.value?.results)
    }

    const getAgreement = async () => {
        const {data} = await useFetch('/api/v1/agreement')
        agreement.value = data.value?.results
        // console.log('agreement:', data)
    }

    const getContract = async () => {
        const {data} = await useFetch('/api/v1/contract')
        contract.value = data.value?.results
        // console.log('contract:', data)
    }

    return {
        organization,
        contractor,
        partner,
        agreement,
        contract,
        getOrganization,
        getContractor,
        getPartner,
        getAgreement,
        getContract
    }
})


