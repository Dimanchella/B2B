import {NuxtAuthHandler} from "#auth";
import CredentialsProvider from "next-auth/providers/credentials";
import {JWT} from "next-auth/jwt";

async function refreshAccessToken(token: JWT) {
    let refreshedTokens;
    try {
        refreshedTokens = await $fetch(
            `${process.env.DJANGO_URL}/backend/api/token/refresh/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: {
                    refresh: token.refreshToken
                }
            }
        )
    } catch (error) {
        throw error
    }

    // @ts-ignore
    if (!refreshedTokens || !refreshedTokens.access) {
        console.error("Ошибка получения обновленного токена")
        throw refreshedTokens;
    }

    return {
        ...token,
        // @ts-ignore
        accessToken: refreshedTokens.access,
        // @ts-ignore
        accessTokenExpires: Date.now() + refreshedTokens.lifetime * 1000,
        // @ts-ignore
        refreshToken: refreshedTokens.refresh
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
            async authorize(credentials: any) {
                try {
                    const payload = {
                        username: credentials.username,
                        password: credentials.password
                    }

                    const userTokens = await $fetch(
                        `${process.env.DJANGO_URL}/backend/api/token/`,
                        {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: payload
                        }
                    )

                    // @ts-ignore
                    if (!userTokens || !userTokens.access) {
                        console.error("Ошибка входа", createError({
                            statusCode: 500,
                            statusMessage: "Ошибка получения JWT-токена"
                        }))
                        return null
                    }

                    const userDetails = await $fetch(
                        `${process.env.DJANGO_URL}/backend/api/v1/user/`,
                        {
                            method: "GET",
                            headers: {
                                "Content-Type": "application/json",
                                // @ts-ignore
                                Authorization: `Bearer ${userTokens?.access}`
                            }
                        }
                    )

                    // @ts-ignore
                    if (!userDetails || !userDetails.user) {
                        console.error("Ошибка входа", createError({
                            statusCode: 500,
                            statusMessage: "Ошибка получения данных пользователя"
                        }))
                        return null
                    }

                    return {
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
                } catch (error) {
                    console.log("Ошибка входа", error)
                    return null
                }
            }
        })
    ],
    callbacks: {
        async jwt({token, user, account}) {
            // @ts-ignore
            if (!(account && user) && (Date.now() > token.accessTokenExpires)) {
                return refreshAccessToken(token)
            }
            return {...token, ...user}
        },

        async session({session, token}) {
            session.user = token
            return session
        }
    },
    pages: {
        signIn: "/auth/signin"
    }
})