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

const iconUrl = require("leaflet/dist/images/marker-icon.png");
const makerIcon = new Icon({ iconUrl: iconUrl, iconSize: [20, 30] });

import { findCountryByName } from "@/utils/countries";
import CountryFlagAndName from "../card/CountryFlagAndName";
import Title from "./Title";

import React from "react";

function PropertyMap({ countryName }: { countryName: string }) {
  const defaultLocation = [51.505, -0.09] as [number, number];
  const location =
    (findCountryByName(countryName)?.location as [number, number]) ||
    defaultLocation;
  return (
    <div className="mt-4">
      <div className="mb-4">
        <Title text="Where you will be staying" />
        <CountryFlagAndName countryCode={countryName} />
      </div>
      <MapContainer
        scrollWheelZoom={false}
        zoomControl={false}
        className="h-[50vh] w-full rounded-lg relative z-0"
        center={location || defaultLocation}
        zoom={7}
        style={{ height: "300px" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <ZoomControl position="bottomright" />
        <Marker
          position={location || defaultLocation}
          icon={makerIcon}
        ></Marker>
      </MapContainer>
    </div>
  );
}

export default PropertyMap;
