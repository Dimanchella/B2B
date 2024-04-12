//  -----------
//  Авторизация
//  -----------
/// js-source
import {NuxtAuthHandler} from "#auth";
import CredentialsProvider from "next-auth/providers/credentials";
import {JWT} from "next-auth/jwt";

// @ts-ignore
async function refreshAccessToken(token: JWT) {
    let refreshedTokens;
    try {
        console.log(">>> Аутентификация. Получение токена доступа")

        const payload = {
            refresh: token.refreshToken,
        }

        refreshedTokens = await $fetch(
            `${process.env.DJANGO_URL}/backend/api/token/refresh/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: payload
            }
        )

        console.log('refreshedTokens:', refreshedTokens)

        // @ts-ignore
        if (!refreshedTokens || !refreshedTokens.access) {
            console.error("!!! Ошибка получения обновленного токена. Токен пустой")
            throw refreshedTokens;
        }

        console.log(">>> Токен получен")

        return {
            ...token,
            // @ts-ignore
            accessToken: refreshedTokens.access,
            // @ts-ignore
            accessTokenExpires: Date.now() + refreshedTokens.lifetime * 1000,
            // @ts-ignore
            refreshToken: refreshedTokens.refresh,
        }
    } catch (error) {
        //throw error
        console.log("!!! Ошибка авторизации")
        throw createError({ statusCode: 403, statusMessage: 'Ошибка обновления токена' })
    }
}

export default NuxtAuthHandler({
    secret: process.env.AUTH_SECRET,
    providers: [
        // @ts-ignore
        CredentialsProvider.default({
            name: 'Credentials',
            credentials: {
                username: {label: "ИНН", type: "text"},
                password: {label: "Пароль", type: "password"}
            },
            async authorize(credentials) {
                console.log('authorize')
                try {
                    const payload = {
                        username: credentials.username,
                        password: credentials.password,
                    }

                    const userTokens = await $fetch(
                        `${process.env.DJANGO_URL}/backend/api/token/`,
                        {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: payload,
                        }
                    )

                    console.log('userTokens:', userTokens, 'payload:', payload)

                    // @ts-ignore
                    if (!userTokens || !userTokens.access) {
                        throw createError({
                            statusCode: 500,
                            statusMessage: "Ошибка получения JWT токена",
                        })
                    }

                    const userDetails = await $fetch(
                        `${process.env.DJANGO_URL}/backend/api/v1/user/`,
                        {
                            method: "GET",
                            headers: {
                                "Content-Type": "application/json",
                                // @ts-ignore
                                Authorization: `Bearer ${userTokens?.access}`,
                            },
                        }
                    )

                    console.log('userDetails:', userDetails)

                    // @ts-ignore
                    if (!userDetails || !userDetails.user) {
                        throw createError({
                            statusCode: 500,
                            statusMessage: "!!! Ошибка получения данных пользователя",
                        })
                    }

                    const userData = {
                        // @ts-ignore
                        username: userDetails.user.username,
                        // @ts-ignore
                        full_name: userDetails.user.full_name,
                        // @ts-ignore
                        accessToken: userTokens.access,
                        // @ts-ignore
                        accessTokenExpires: Date.now() + userTokens.lifetime * 1000,
                        // @ts-ignore
                        refreshToken: userTokens.refresh
                    }
                    
                    console.log('userData:', userData)

                    return userData
                } catch (error) {
                    console.log("!!! Ошибка входа", error)
                    return null
                }
            }
        })
    ],
    callbacks: {
        // @ts-ignore
        async jwt({ token, user, account }) {

            console.log('jwt...', 'user:', user, 'account:', account, 'token:', token)

            if (account && user) {
                console.log('>>> Пользователь авторизован (with account)')
                return { ...token, ...user }
            }

            else if (token && !isNaN(token.accessTokenExpires) && Date.now() > token.accessTokenExpires) {
                console.log(">>> Срок действия токена истек. Получение нового")
                // @ts-ignore
                return refreshAccessToken(token)
            }   
            else if (token && user) {
                console.log('>>> Пользователь авторизован')
            }
            return { ...token, ...user }
        },

        // @ts-ignore
         async session({ session, token }) {
            console.log('>>> Чтение сессии', 'session:', session, 'token:',  token)
            session.user = token
            return session
        },
        /*
        // @ts-ignore
        async session({ session, user, token }) {
            if (token && typeof token.accessTokenExpire === 'number' && typeof token.accessTokenIssuedAt === 'number') {
                const tempsession: any = session;
                // session interval in seconds, It's accesstoken expire - 10 minutes
                let interval = Math.round(((token.accessTokenExpire - token.accessTokenIssuedAt) - (60000 * 10)) / 1000);
                if (interval < 300) {
                    interval = 2
                }
                tempsession.interval = interval;
                return tempsession;
            } else {
                return session;
            }
        }
        */
    },
    pages: {
        signIn: '/auth/signin',
    },
})
