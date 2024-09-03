export type actionFunction = (
  prevState: any,
  formDate: FormData
) => Promise<{ message: string }>;
