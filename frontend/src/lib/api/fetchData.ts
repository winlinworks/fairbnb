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
    `${process.env.NEXT_PUBLIC_API_URL}/listings/${id}`,
    { cache: "no-cache" }
  );
  const post = await data.json();
  return post;
};