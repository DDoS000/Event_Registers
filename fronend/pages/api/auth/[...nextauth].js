import NextAuth from "next-auth"
import Providers from "next-auth/providers"
import axios from 'axios';

const options = {
  providers: [
    Providers.Credentials({
      // The name to display on the sign in form (e.g. 'Sign in with...')
      name: 'JWT',
      // The credentials property is used to generate a suitable form on the sign in page.
      credentials: {
        username: { label: "Email", type: "email", placeholder: "Email" },
        password: {  label: "Password", type: "password" }
      },
      async authorize(credentials) {
        try {
            const user = axios.post(`${process.env.NEXT_PUBLIC_APP_BACKEND_URL}api/v1/login`, {
                username: credentials.username,
                password: credentials.password
              })
          if (user) {
            console.log(user.data);
            return user.data;
          } else {
            return null;
          }
        } catch(e) {
          throw new Error("There was an error on user authentication");  
        }
      }
    })    
  ],
}

export default (req, res) => NextAuth(req, res, options);
