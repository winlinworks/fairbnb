export type actionFunction = (
  prevState: any,
  formDate: FormData
) => Promise<{ message: string }>;

export type PropertyCardProps = {
  image: string;
  id: string;
  name: string;
  tagline: string;
  location: string;
  price: number;
};
