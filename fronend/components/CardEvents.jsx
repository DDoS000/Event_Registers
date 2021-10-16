import * as React from "react";
import PropTypes from "prop-types";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardActionArea from "@mui/material/CardActionArea";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import { styled, Box } from "@mui/system";
import ModalUnstyled from "@mui/core/ModalUnstyled";
import Link from "next/link";

const StyledModal = styled(ModalUnstyled)`
  position: fixed;
  z-index: 1300;
  right: 0;
  bottom: 0;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Backdrop = styled("div")`
  z-index: -1;
  position: fixed;
  right: 0;
  bottom: 0;
  top: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.5);
  -webkit-tap-highlight-color: transparent;
`;

const style = {
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  p: 2,
  px: 4,
  pb: 3,
};

function CardEvents(props) {
  const { events } = props;
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <Grid item xs={12} md={6}>
      <CardActionArea component="a" onClick={handleOpen}>
        <Card sx={{ display: "flex" }}>
          <CardContent sx={{ flex: 1 }}>
            <Typography component="h2" variant="h5">
              {events.name}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              {events.start_date}
            </Typography>
            <Typography variant="subtitle1" paragraph>
              {events.description}
            </Typography>
            <Typography variant="subtitle1" paragraph>
              {events.location}
            </Typography>
          </CardContent>
          <CardMedia
            component="img"
            sx={{ width: 160, display: { xs: "none", sm: "block" } }}
            image={events.image}
            alt={events.name}
          />
        </Card>
      </CardActionArea>
      <StyledModal
        aria-labelledby="unstyled-modal-title"
        aria-describedby="unstyled-modal-description"
        open={open}
        onClose={handleClose}
        BackdropComponent={Backdrop}
      >
        <Box sx={style}>
          <h2 id="unstyled-modal-title">ติดตาม {events.name}</h2>
          <p id="unstyled-modal-description">
            เวลาเริ่มกิจกรรม {events.start_date}
          </p>
          <Link
            href={{
              pathname: "https://notify-bot.line.me/oauth/authorize",
              query: {
                response_type: "code",
                client_id: 'FykzC8Av9e9DGP23viU8AS',
                redirect_uri: 'http://localhost:3000/success',
                scope: "notify",
                state: `${events.id}`,
              },
            }}
          >
            <Button color="primary" variant="contained">
              ติดตามผ่าน Line notify
            </Button>
          </Link>
        </Box>
      </StyledModal>
    </Grid>
  );
}

CardEvents.propTypes = {
  events: PropTypes.shape({
    name: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    location: PropTypes.string.isRequired,
    start_date: PropTypes.string.isRequired,
    end_date: PropTypes.string.isRequired,
    created_by: PropTypes.number.isRequired,
    created_on: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    image: PropTypes.string.isRequired,
  }).isRequired,
};

export default CardEvents;
