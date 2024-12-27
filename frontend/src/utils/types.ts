export type actionFunction = (
  prevState: any,
  formDate: FormData
) => Promise<{ message: string }>;

export type PropertyCardProps = {
  image: string;
  id: number;
  name: string;
  tagline: string;
  location: string;
  price: number;
};
