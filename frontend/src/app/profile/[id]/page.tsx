"use client";

import { useEffect, useState } from "react";
import { fetchUserInfo } from "@/lib/api/fetchData";
import { updateProfileAction } from "@/lib/api/updateData";

import FormContainer from "@/components/form/FormContainer";
import FormInput from "@/components/form/FormInput";
import SubmitButton from "@/components/form/Buttons";
import { set } from "date-fns";

function ProfilePage({ params }: { params: { id: string } }) {
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchUserInfo(params.id);
        setProfile(data);
      } catch (error) {
        console.error("Failed to fetch profile", error);
      }
    };
    fetchData();
  }, [params.id]);
  if (!profile) return <p>Loading...</p>;

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
              placeholder="First Name"
            />
            <FormInput
              type="text"
              name="lastName"
              label="Last Name"
              defaultValue={profile.lastName}
            />

            <FormInput
              type="text"
              name="email"
              label="Email address"
              defaultValue={profile.email}
            />
            <SubmitButton text="Update Profile" className="mt-8" />
          </div>
        </FormContainer>
      </div>
    </section>
  );
}
export default ProfilePage;
