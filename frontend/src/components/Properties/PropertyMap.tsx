"use client";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  ZoomControl,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { Icon } from "leaflet";

const markerIconUrl = require("leaflet/dist/images/marker-icon.png");
const markerShadowUrl = require("leaflet/dist/images/marker-shadow.png");

const makerIcon = new Icon({
  iconUrl: markerIconUrl,
  shadowUrl: markerShadowUrl,
  iconSize: [20, 30],
});

import { findCountryByName } from "@/utils/countries";
import CountryFlagAndName from "../card/CountryFlagAndName";
import Title from "./Title";

function PropertyMap({ countryName }: { countryName: string }) {
  const defaultLocation = [51.505, -0.09] as [number, number];
  const location =
    (findCountryByName(countryName)?.location as [number, number]) ||
    defaultLocation;
  return (
    <div className="mt-4">
      <div className="mb-4">
        <Title text="Where you will be staying" />
        <CountryFlagAndName countryName={countryName} />
      </div>
      <MapContainer
        scrollWheelZoom={true}
        zoomControl={false}
        className="h-[50vh] w-full rounded-lg relative z-0"
        center={location || defaultLocation}
        zoom={7}
        style={{ height: "300px" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        <Marker position={location || defaultLocation} icon={makerIcon}>
          <Popup> {countryName || "Unknown Location"}</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

export default PropertyMap;
