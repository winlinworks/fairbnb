"use server";

import { profileSchema } from "./schemas";
import axios from "axios";

// Define the API endpoint
const API_URL = 'http://backend:8000';

export const createProfileAction = async (
  prevState: any,
  formData: FormData
) => {
  try {
    const rawData = Object.fromEntries(formData);
    const validatedFields = profileSchema.parse(rawData);
    console.log(validatedFields);
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
  const properties = getListings("1");
  return properties;
};

// Function to get listings data from the API
async function getListings(
  userId: string,
) {
  const listingsUrl = `${API_URL}/listings`;

  // Get listings from the API and return them, or return an empty array if there's an error
  try {
    const response = await axios.get(listingsUrl);
    return response.data;
  } catch (error) {
    console.error('Error fetching properties:', error);
    return [];
  }
}
