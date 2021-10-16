import axios from "axios";

export default async (req, res) => {
    res.statusCode = 200
    try {
        const data = req.body;
        const params = new URLSearchParams();
        params.append('message', data.message);
        const request = await axios.post("https://notify-api.line.me/api/notify", params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${data.token}`,
            }
        })
        console.log(request.data);
    } catch (e) {
        console.log(e);
    }
    res.json({ status: 'OK' })
}