"use server";

import { profileSchema } from "./schemas";

const MockProperty = [
  {
    id: 1,
    name: "property-1",
    tagline: "this is property 1",
    location: "Houston, TX",
    image:
      "https://a0.muscache.com/im/pictures/2adf6ef9-e131-431b-a34e-9566e768f509.jpg?im_w=1200",
    price: 314,
  },
  {
    id: 2,
    name: "property-2",
    tagline: "this is property 2",
    location: "Houston, TX",
    image:
      "https://a0.muscache.com/im/pictures/2f53e928-a91e-464c-b69f-14eff28a3b85.jpg?im_w=960",
    price: 263,
  },
  {
    id: 3,
    name: "property-3",
    tagline: "this is property 3",
    location: "Houston, TX",
    image:
      "https://a0.muscache.com/im/pictures/d1db0b4a-9830-42e2-875d-0d41820ca4e3.jpg?im_w=960",
    price: 180,
  },
  {
    id: 4,
    name: "property-4",
    tagline: "this is property 4",
    location: "Houston, TX",
    image:
      "https://a0.muscache.com/im/pictures/d1db0b4a-9830-42e2-875d-0d41820ca4e3.jpg?im_w=960",
    price: 180,
  },
  {
    id: 5,
    name: "property-5",
    tagline: "this is property 5",
    location: "Houston, TX",
    image:
      "https://a0.muscache.com/im/pictures/d1db0b4a-9830-42e2-875d-0d41820ca4e3.jpg?im_w=960",
    price: 180,
  },
];

export const createProfileAction = async (
  prevState: any,
  formData: FormData
) => {
  try {
    const rawData = Object.fromEntries(formData);
    const validedFields = profileSchema.parse(rawData);
    console.log(validedFields);
    return { message: "profile created" };
  } catch (error) {
    console.log(error);
    return { message: "there was an error" };
  }
};

export const fetchProperties = async ({
  search = "",
  category,
}: {
  search?: string;
  category?: string;
}) => {
  const properties = MockProperty;
  return properties;
};
