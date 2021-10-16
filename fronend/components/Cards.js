import useSWR, { SWRConfig } from "swr";
import CardEvents from '../components/CardEvents'
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';

const fetcher = (url) => fetch(url).then((res) => res.json());
const API = `${process.env.NEXT_PUBLIC_APP_BACKEND_URL}api/v1/events`;


export default function CEvents() {
    const { data, error } = useSWR(API, fetcher);

    console.log("Is data ready?", !!data);

    if (error) return "An error has occurred.";
    if (!data) return "Loading...";
    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
                {data.map((data) => (
                    <CardEvents key={data.id} events={data} />
                ))}
            </Grid>
        </Container>
    );
}