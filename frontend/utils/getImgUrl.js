export default (url) => {
    const runtimeConfig = useRuntimeConfig()
    //return runtimeConfig.public.imgUrl + url
    return 'http://localhost:8000/' + url
}
