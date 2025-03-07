"use server";

export const fetchPropertiesListings = async () => {
  const data = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/listings`, {
    cache: "no-store",
  });
  const posts = await data.json();
  return posts;
};

export const fetchPropertyDetails = async (id: number) => {
  const data = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/propertyDetails/${id}`,
    { cache: "no-cache" }
  );
  const post = await data.json();
  return post;
};

export const fetchUserInfo = async (id: string) => {
  const data = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/profiles/${id}`,
    {
      cache: "no-cache",
    }
  );
  const user = await data.json();
  return user;
};
