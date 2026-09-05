import { NotAvailable } from './errors';

export class TranslationService {
  constructor(api) {
    this.api = api;
  }

  free(text) {
    return this.api.fetch(text)
      .then(result => {
        return result.translation;
      });
  }

  batch(texts) {
    if (texts.length === 0) {
      return Promise.reject(new BatchIsEmpty());
    }

    return Promise.all(
      texts.map(text => this.free(text))
    );
  }

  request(text) {
    return new Promise((resolve, reject) => {
      let attempts = 0;

      const tryRequest = () => {
        attempts++;

        this.api.request(text, error => {
          if (error === undefined) {
            resolve();
          } else if (attempts < 3) {
            tryRequest();
          } else {
            reject(error);
          }
        });
      };

      tryRequest();
    });
  }

  premium(text, minimumQuality) {
    return this.api.fetch(text)
      .then(result => {
        if (result.quality >= minimumQuality) {
          return result.translation;
        }

        throw new QualityThresholdNotMet(text);
      })
      .catch(error => {
        if (error instanceof NotAvailable) {
          return this.request(text)
            .then(() => this.premium(text, minimumQuality));
        }

        throw error;
      });
  }
}
export class QualityThresholdNotMet extends Error {
  /**
   * @param {string} text
   */
  constructor(text) {
    super(
      `
The translation of ${text} does not meet the requested quality threshold.
    `.trim(),
    );

    this.text = text;
  }
}

/**
 * This error is used to indicate the batch service was called without any
 * texts to translate (it was empty). Do not change the name of this error.
 */
export class BatchIsEmpty extends Error {
  constructor() {
    super(
      `
Requested a batch translation, but there are no texts in the batch.
    `.trim(),
    );
  }
}
