import { FileManager } from "./FileManager";

export class FileService {
  constructor(private manager: FileManager) {}

  getFile(bucket: string, key: string, provider: string, region: string, retries: number, timeoutMs: number) {
    return this.manager.getFile(bucket, key, provider, region, retries, timeoutMs);
  }

  deleteFile(bucket: string, key: string, provider: string, region: string, retries: number, timeoutMs: number) {
    return this.manager.deleteFile(bucket, key, provider, region, retries, timeoutMs);
  }
}
