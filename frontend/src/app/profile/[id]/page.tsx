import React from "react";
import { fetchUserInfo } from "@/lib/api/fetchData";

import FormContainer from "@/components/form/FormContainer";
import FormInput from "@/components/form/FormInput";
import SubmitButton from "@/components/form/Buttons";
import { updateProfileAction } from "@/lib/api/updateData";

async function ProfilePage({ params }: { params: { id: string } }) {
  const profile = await fetchUserInfo(params.id);

  return (
    <section>
      <h1 className="text-2xl font-semibold mb-8 capitalize">user profile</h1>
      <div className="border p-8 rounded-md">
        {/* image input container */}

        <FormContainer action={updateProfileAction}>
          <div className="grid gap-4 md:grid-cols-1 mt-4">
            <FormInput
              type="text"
              name="firstName"
              label="First Name"
              defaultValue={profile.firstName}
            />
            <FormInput
              type="text"
              name="lastName"
              label="Last Name"
              defaultValue={profile.lastName}
            />
            <FormInput
              type="text"
              name="username"
              label="Username"
              defaultValue={profile.username}
            />
            <FormInput
              type="text"
              name="email"
              label="Email address"
              defaultValue={profile.email}
            />
          </div>
          <SubmitButton text="Update Profile" className="mt-8" />
        </FormContainer>
      </div>
    </section>
  );
}
export default ProfilePage;
