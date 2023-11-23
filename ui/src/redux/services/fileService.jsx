import { instance } from "./Instance";

async function fileImport(file,id,docType,sweepCount) {
    const category = (docType=== "1") ? "UI" : "API";
    try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await instance.post(`report/testcaseImport/${id}/${sweepCount}/${category}/`, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });

        return response;
    } catch (error) {
        return error.response;
    }
}


async function fileExport(projectId) {
    try {
        const response = await instance.get(`report/export/${projectId}`);
        return response.data; 
    } catch (error) {
        return error;
    }
}

export const fileService = {
    fileImport,
    fileExport
};
