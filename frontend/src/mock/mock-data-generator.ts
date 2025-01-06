import { profiles } from "./models/profiles";
import { properties } from "./models/properties";
import { propertyDetails } from "./models/propertyDetails";
import { writeFile } from "fs";

writeFile(
  "src/mock/data.json",
  JSON.stringify({
    profiles: profiles,
    properties: properties,
    propertyDetails: propertyDetails,
  }),
  function (err: any) {
    if (err) {
      console.log(err);
    }
  }
);
