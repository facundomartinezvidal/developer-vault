import { S3Client, GetObjectCommand, DeleteObjectCommand, HeadObjectCommand } from "@aws-sdk/client-s3";

export class FileManager {
  private client?: S3Client;

  init(region: string, retries: number, timeoutMs: number) {
    this.client = new S3Client({ region, maxAttempts: retries, requestHandler: { requestTimeout: timeoutMs } as any });
  }

  async getFile(bucket: string, key: string, provider: string, region: string, retries: number, timeoutMs: number) {
    if (provider !== "aws") throw new Error("unsupported provider");
    this.init(region, retries, timeoutMs);
    return this.client!.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
  }

  async deleteFile(bucket: string, key: string, provider: string, region: string, retries: number, timeoutMs: number) {
    if (provider !== "aws") throw new Error("unsupported provider");
    this.init(region, retries, timeoutMs);
    await this.client!.send(new HeadObjectCommand({ Bucket: bucket, Key: key }));
    return this.client!.send(new DeleteObjectCommand({ Bucket: bucket, Key: key }));
  }
}
