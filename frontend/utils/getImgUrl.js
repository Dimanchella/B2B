export default (url) => {
    const runtimeConfig = useRuntimeConfig()
    console.log(runtimeConfig.public.imgUrl + url)
    return runtimeConfig.public.imgUrl + url
    // return 'http://localhost:8000/' + url
}
