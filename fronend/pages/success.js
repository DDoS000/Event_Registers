import React, { Component } from 'react';
import axios from "axios";
import Container from '@mui/material/Container'
import Button from '@mui/material/Button'
import Link from 'next/link';

const useStyle = theme => ({
    root: {
        height: "100vh",
        paddingTop: theme.spacing(4)
    },
    paper: {
        padding: theme.spacing(2)
    },
    button: {
        width: "100%"
    }
});

class Success extends Component {

    static async getInitialProps(ctx) {
        const { query } = ctx;
        console.log(query);
        let data;
        try {
            if (query.code) {
                const params = new URLSearchParams();
                params.append('grant_type', 'authorization_code');
                params.append('code', query.code);
                params.append('redirect_uri', 'http://localhost:3000/success');
                params.append('client_id', 'FykzC8Av9e9DGP23viU8AS');
                params.append('client_secret', 'cG5r8rRyY5oNBqwKJC8Mr1HnwhwJTHFD2BigS4UlAnk');

                const request = await axios.post("https://notify-bot.line.me/oauth/token", params, {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                data = request.data;

                // Store access token
                axios.post(
                    `${process.env.NEXT_PUBLIC_APP_BACKEND_URL}api/v1/events_register`,
                    {
                        events_id: query.state,
                        code: query.code,
                        token: data.access_token,
                    },
                    {
                        headers: {
                            "Content-Type": "application/json"
                        },
                    }
                )
                    .then((response) => {
                        console.log("response: ", response);
                    })
                    .catch((err) => {
                        console.error(err);
                    });
            }
        } catch (e) {
            console.log(e);
        }
        return {
            code: query.code,
            token: data?.access_token
        }
    }

    constructor(props) {
        super(props)
    }

    async handlerClick() {
        const { classes, token } = this.props;
        if (token) {
            try {
                const request = await axios.post("/api/notify", {
                    token: token,
                    message: "ได้ทําการสมัครเรียบร้อยแล้ว"
                })
            } catch (e) {

            }
        }
    }

    render() {
        return (
            <Container >
                <Link href="/">
                    <Button
                        color='primary'
                        onClick={() => this.handlerClick()}
                        variant="contained">
                        Back
                    </Button>
                </Link>
            </Container>
        )
    }
}

export default Success;