import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpamCheck } from './spam-check';

describe('SpamCheck', () => {
  let component: SpamCheck;
  let fixture: ComponentFixture<SpamCheck>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpamCheck]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpamCheck);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
