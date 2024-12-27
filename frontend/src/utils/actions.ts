"use server";

import { profileSchema } from "./schemas";

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
  const data = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/listings`, {
    cache: 'no-store'
  });
  const posts = await data.json();

  // const properties = mockProperty;
  const properties = posts
  return properties;
};
